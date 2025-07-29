#!/usr/bin/env python3
import ast,sys,json,logging,re
from pathlib import Path
from collections import defaultdict
from skylos.visitor import Visitor
from skylos.constants import (
    AUTO_CALLED, TEST_METHOD_PATTERN, MAGIC_METHODS,
    TEST_LIFECYCLE_METHODS, TEST_IMPORT_PATTERNS, TEST_DECORATORS,
    DEFAULT_EXCLUDE_FOLDERS
)

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger('Skylos')

def parse_exclude_folders(user_exclude_folders, use_defaults=True, include_folders=None):
    exclude_set = set()
    
    if use_defaults:
        exclude_set.update(DEFAULT_EXCLUDE_FOLDERS)
        
    if user_exclude_folders:
        exclude_set.update(user_exclude_folders)
    
    if include_folders:
        for folder in include_folders:
            exclude_set.discard(folder)
    
    return exclude_set

class Skylos:
    def __init__(self):
        self.defs={}
        self.refs=[]
        self.dynamic=set()
        self.exports=defaultdict(set)

    def _module(self,root,f):
        p=list(f.relative_to(root).parts)
        if p[-1].endswith(".py"):p[-1]=p[-1][:-3]
        if p[-1]=="__init__":p.pop()
        return".".join(p)
    
    def _should_exclude_file(self, file_path, root_path, exclude_folders):
        if not exclude_folders:
            return False
            
        try:
            rel_path = file_path.relative_to(root_path)
        except ValueError:
            return False
        
        path_parts = rel_path.parts
        
        for exclude_folder in exclude_folders:
            if "*" in exclude_folder:
                for part in path_parts:
                    if part.endswith(exclude_folder.replace("*", "")):
                        return True
            else:
                if exclude_folder in path_parts:
                    return True
        
        return False
    
    def _get_python_files(self, path, exclude_folders=None):
        p = Path(path).resolve()
        
        if p.is_file():
            return [p], p.parent
        
        root = p
        all_files = list(p.glob("**/*.py"))
        
        if exclude_folders:
            filtered_files = []
            excluded_count = 0
            
            for file_path in all_files:
                if self._should_exclude_file(file_path, root, exclude_folders):
                    excluded_count += 1
                    continue
                filtered_files.append(file_path)
            
            if excluded_count > 0:
                logger.info(f"Excluded {excluded_count} files from analysis")
            
            return filtered_files, root
        
        return all_files, root
    
    def _mark_exports(self):
        for name, d in self.defs.items():
            if d.in_init and not d.simple_name.startswith('_'):
                d.is_exported = True
        
        for mod, export_names in self.exports.items():
            for name in export_names:
                for def_name, def_obj in self.defs.items():
                    if (def_name.startswith(f"{mod}.") and 
                        def_obj.simple_name == name and
                        def_obj.type != "import"):
                        def_obj.is_exported = True

    def _mark_refs(self):
        import_to_original = {}
        for name, def_obj in self.defs.items():
            if def_obj.type == "import":
                import_name = name.split('.')[-1]
                
                for def_name, orig_def in self.defs.items():
                    if (orig_def.type != "import" and 
                        orig_def.simple_name == import_name and
                        def_name != name):
                        import_to_original[name] = def_name
                        break

        simple_name_lookup = defaultdict(list)
        for d in self.defs.values():
            simple_name_lookup[d.simple_name].append(d)
        
        for ref, _ in self.refs:
            if ref in self.defs:
                self.defs[ref].references += 1
                
                if ref in import_to_original:
                    original = import_to_original[ref]
                    self.defs[original].references += 1
                continue
            
            simple = ref.split('.')[-1]
            matches = simple_name_lookup.get(simple, [])
            for d in matches:
                d.references += 1
    
    def _get_base_classes(self, class_name):
        if class_name not in self.defs:
            return []
        
        class_def = self.defs[class_name]
        
        if hasattr(class_def, 'base_classes'):
            return class_def.base_classes
        
        return []
    
    def _has_test_imports(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for test_import in TEST_IMPORT_PATTERNS:
                if f"import {test_import}" in content or f"from {test_import}" in content:
                    return True
                    
            return False
        except:
            return False
    
    def _is_test_file(self, file_path):
        """check if file locs indicates its a test file"""
        file_str = str(file_path).lower()
        
        if (file_str.endswith("test.py") or 
            file_str.endswith("_test.py") or 
            "test_" in file_str or
            "/test/" in file_str or
            "/tests/" in file_str or
            "\\test\\" in file_str or
            "\\tests\\" in file_str):
            return True
            
        return False

    def _has_test_decorators(self, file_path):
        """Check if file uses test-related decorators"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for decorator in TEST_DECORATORS:
                if f"@{decorator}" in content:
                    return True
                    
            return False
        except:
            return False
        
    def _is_test_related(self, definition):
        
        if "." in definition.name:
            class_name = definition.name.rsplit(".", 1)[0]
            class_simple_name = class_name.split(".")[-1]
            
            if (class_simple_name.startswith("Test") or 
                class_simple_name.endswith("Test") or 
                class_simple_name.endswith("TestCase")):
                return True
        
        if (definition.type == "method" and 
            (TEST_METHOD_PATTERN.match(definition.simple_name) or
             definition.simple_name in TEST_LIFECYCLE_METHODS)):
            return True
        
        # NOT for imports, variables, parameters
        if definition.type in ("function", "method", "class"):
            if self._is_test_file(definition.filename):
                return True
                
            if self._has_test_imports(definition.filename):
                return True
                
            ## check decorators -- test related
            if self._has_test_decorators(definition.filename):
                return True
            
        return False
                    
    def _apply_heuristics(self):
        class_methods=defaultdict(list)
        for d in self.defs.values():
            if d.type in("method","function") and"." in d.name:
                cls=d.name.rsplit(".",1)[0]
                if cls in self.defs and self.defs[cls].type=="class":
                    class_methods[cls].append(d)

        for cls,methods in class_methods.items():
            if self.defs[cls].references>0:
                for m in methods:
                    if m.simple_name in AUTO_CALLED:m.references+=1
                    
        for d in self.defs.values():
            if d.simple_name in MAGIC_METHODS or (d.simple_name.startswith("__") and d.simple_name.endswith("__")):
                d.confidence = 0
            
            if d.type == "parameter" and d.simple_name in ("self", "cls"):
                d.confidence = 0

            if d.type != "parameter" and (d.simple_name in MAGIC_METHODS or (d.simple_name.startswith("__") and d.simple_name.endswith("__"))):
                d.confidence = 0

            if (d.type == "import" and d.name.startswith("__future__.") and
                d.simple_name in ("annotations", "absolute_import", "division", 
                                "print_function", "unicode_literals", "generator_stop")):
                d.confidence = 0

            if (d.simple_name.startswith("_") and 
                not d.simple_name.startswith("__") and  
                d.simple_name != "_"):
                d.confidence = 0

            if not d.simple_name.startswith("_") and d.type in ("function", "method", "class"):
                d.confidence = min(d.confidence, 90)
            
            if d.in_init and d.type in ("function", "class"):
                d.confidence = min(d.confidence, 85)
            
            if d.name.split(".")[0] in self.dynamic:
                d.confidence = min(d.confidence, 60)
            
            if d.type == "variable" and d.simple_name == "_":
                d.confidence = 0
            
            if self._is_test_related(d):
                d.confidence = 0

    def analyze(self, path, thr=60, exclude_folders=None):
        
        files, root = self._get_python_files(path, exclude_folders)
        
        if not files:
            logger.warning(f"No Python files found in {path}")
            return json.dumps({
                "unused_functions": [], 
                "unused_imports": [], 
                "unused_classes": [],
                "unused_variables": [],
                "unused_parameters": [],
                 "analysis_summary": {
                    "total_files": 0,
                    "excluded_folders": exclude_folders if exclude_folders else []
                }
            })
        
        logger.info(f"Analyzing {len(files)} Python files...")
        
        modmap = {}
        for f in files:
            modmap[f] = self._module(root, f)
        
        for file in files:
            mod = modmap[file]
            defs, refs, dyn, exports = proc_file(file, mod)
            
            for d in defs: 
                self.defs[d.name] = d
            self.refs.extend(refs)
            self.dynamic.update(dyn)
            self.exports[mod].update(exports)
        
        self._mark_refs()
        self._apply_heuristics()
        self._mark_exports()
                
        thr = max(0, thr)

        unused = []
        for d in self.defs.values():
            if d.references == 0 and not d.is_exported and d.confidence >= thr:
                unused.append(d.to_dict())
        
        result = {
            "unused_functions": [], 
            "unused_imports": [], 
            "unused_classes": [],
            "unused_variables": [],
            "unused_parameters": [],
            "analysis_summary": {
                "total_files": len(files),
                "excluded_folders": exclude_folders if exclude_folders else [],
            }
        }
        
        for u in unused:
            if u["type"] in ("function", "method"):
                result["unused_functions"].append(u)
            elif u["type"] == "import":
                result["unused_imports"].append(u)
            elif u["type"] == "class": 
                result["unused_classes"].append(u)
            elif u["type"] == "variable":
                result["unused_variables"].append(u)
            elif u["type"] == "parameter":
                result["unused_parameters"].append(u)
                
        return json.dumps(result, indent=2)

def proc_file(file_or_args, mod=None):
    if mod is None and isinstance(file_or_args, tuple):
        file, mod = file_or_args 
    else:
        file = file_or_args 

    try:
        tree = ast.parse(Path(file).read_text(encoding="utf-8"))
        v = Visitor(mod, file)
        v.visit(tree)
        return v.defs, v.refs, v.dyn, v.exports
    except Exception as e:
        logger.error(f"{file}: {e}")
        return [], [], set(), set()

def analyze(path,conf=60, exclude_folders=None):
    return Skylos().analyze(path,conf, exclude_folders)

if __name__=="__main__":
    if len(sys.argv)>1:
        p=sys.argv[1];c=int(sys.argv[2])if len(sys.argv)>2 else 60
        result = analyze(p,c)
        
        data = json.loads(result)
        print("\n🔍 Python Static Analysis Results")
        print("===================================\n")
        
        total_items = sum(len(items) for items in data.values())
        
        print("Summary:")
        if data["unused_functions"]:
            print(f"  • Unreachable functions: {len(data['unused_functions'])}")
        if data["unused_imports"]:
            print(f"  • Unused imports: {len(data['unused_imports'])}")
        if data["unused_classes"]:
            print(f"  • Unused classes: {len(data['unused_classes'])}")
        if data["unused_variables"]:
            print(f"  • Unused variables: {len(data['unused_variables'])}")
        
        if data["unused_functions"]:
            print("\n📦 Unreachable Functions")
            print("=======================")
            for i, func in enumerate(data["unused_functions"], 1):
                print(f" {i}. {func['name']}")
                print(f"    └─ {func['file']}:{func['line']}")
        
        if data["unused_imports"]:
            print("\n📥 Unused Imports")
            print("================")
            for i, imp in enumerate(data["unused_imports"], 1):
                print(f" {i}. {imp['simple_name']}")
                print(f"    └─ {imp['file']}:{imp['line']}")
        
        if data["unused_classes"]:
            print("\n📋 Unused Classes")
            print("=================")
            for i, cls in enumerate(data["unused_classes"], 1):
                print(f" {i}. {cls['name']}")
                print(f"    └─ {cls['file']}:{cls['line']}")
                
        if data["unused_variables"]:
            print("\n📊 Unused Variables")
            print("==================")
            for i, var in enumerate(data["unused_variables"], 1):
                print(f" {i}. {var['name']}")
                print(f"    └─ {var['file']}:{var['line']}")
        
        print("\n" + "─" * 50)
        print(f"Found {total_items} dead code items. Add this badge to your README:")
        print(f"```markdown")
        print(f"![Dead Code: {total_items}](https://img.shields.io/badge/Dead_Code-{total_items}_detected-orange?logo=codacy&logoColor=red)")
        print(f"```")
        
        print("\nNext steps:")
        print("  • Use --interactive to select specific items to remove")
        print("  • Use --dry-run to preview changes before applying them")
    else:
        print("Usage: python Skylos.py <path> [confidence_threshold]")