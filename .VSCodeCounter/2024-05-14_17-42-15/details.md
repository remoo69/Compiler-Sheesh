# Details

Date : 2024-05-14 17:42:15

Directory c:\\Users\\anton\\Desktop\\compiler_sheesh

Total : 56 files,  13826 codes, 1242 comments, 3048 blanks, all 18116 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 60 | 0 | 10 | 70 |
| [compiler_sheesh.cfg](/compiler_sheesh.cfg) | Properties | 13 | 0 | 1 | 14 |
| [requirements.txt](/requirements.txt) | pip requirements | 7 | 0 | 0 | 7 |
| [source/CodeGeneration/CodeGen.py](/source/CodeGeneration/CodeGen.py) | Python | 160 | 65 | 60 | 285 |
| [source/CodeGeneration/CodeOptimizer.py](/source/CodeGeneration/CodeOptimizer.py) | Python | 2 | 0 | 2 | 4 |
| [source/CodeGeneration/Functionality/ControlFlow.py](/source/CodeGeneration/Functionality/ControlFlow.py) | Python | 72 | 10 | 17 | 99 |
| [source/CodeGeneration/Functionality/Declarations.py](/source/CodeGeneration/Functionality/Declarations.py) | Python | 38 | 6 | 12 | 56 |
| [source/CodeGeneration/Functionality/Evaluators.py](/source/CodeGeneration/Functionality/Evaluators.py) | Python | 378 | 25 | 50 | 453 |
| [source/CodeGeneration/Functionality/Functionality.py](/source/CodeGeneration/Functionality/Functionality.py) | Python | 36 | 8 | 30 | 74 |
| [source/CodeGeneration/Functionality/InOut.py](/source/CodeGeneration/Functionality/InOut.py) | Python | 107 | 18 | 18 | 143 |
| [source/CodeGeneration/Functionality/Loops.py](/source/CodeGeneration/Functionality/Loops.py) | Python | 51 | 27 | 20 | 98 |
| [source/CodeGeneration/Functionality/Variables.py](/source/CodeGeneration/Functionality/Variables.py) | Python | 12 | 2 | 10 | 24 |
| [source/CodeGeneration/Functionality/__init__.py](/source/CodeGeneration/Functionality/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [source/CodeGeneration/IntermediateCodeGen.py](/source/CodeGeneration/IntermediateCodeGen.py) | Python | 259 | 53 | 66 | 378 |
| [source/CodeGeneration/__init__.py](/source/CodeGeneration/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [source/LexicalAnalyzer/Lexer.py](/source/LexicalAnalyzer/Lexer.py) | Python | 138 | 2 | 27 | 167 |
| [source/LexicalAnalyzer/__init__.py](/source/LexicalAnalyzer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [source/LexicalAnalyzer/prepare.py](/source/LexicalAnalyzer/prepare.py) | Python | 388 | 2 | 88 | 478 |
| [source/SemanticAnalyzer/SemanticAnalyzer.py](/source/SemanticAnalyzer/SemanticAnalyzer.py) | Python | 276 | 347 | 176 | 799 |
| [source/SemanticAnalyzer/Semantisizer.py](/source/SemanticAnalyzer/Semantisizer.py) | Python | 76 | 4 | 24 | 104 |
| [source/Sheesh# Compiler.py](/source/Sheesh#%20Compiler.py) | Python | 430 | 42 | 120 | 592 |
| [source/SyntaxAnalyzer/Parser.py](/source/SyntaxAnalyzer/Parser.py) | Python | 2,087 | 84 | 322 | 2,493 |
| [source/SyntaxAnalyzer/__init__.py](/source/SyntaxAnalyzer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [source/SyntaxAnalyzer/parser2.py](/source/SyntaxAnalyzer/parser2.py) | Python | 2,274 | 48 | 372 | 2,694 |
| [source/__init__.py](/source/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [source/core/AST.py](/source/core/AST.py) | Python | 148 | 34 | 50 | 232 |
| [source/core/__init__.py](/source/core/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [source/core/compile.py](/source/core/compile.py) | Python | 54 | 2 | 19 | 75 |
| [source/core/constants.py](/source/core/constants.py) | Python | 295 | 9 | 73 | 377 |
| [source/core/error_handler.py](/source/core/error_handler.py) | Python | 382 | 11 | 39 | 432 |
| [source/core/error_types.py](/source/core/error_types.py) | Python | 93 | 4 | 50 | 147 |
| [source/core/std.py](/source/core/std.py) | Python | 6 | 0 | 2 | 8 |
| [source/core/symbol_table.py](/source/core/symbol_table.py) | Python | 236 | 21 | 89 | 346 |
| [src/source/README.md](/src/source/README.md) | Markdown | 28 | 0 | 17 | 45 |
| [src/source/compiler_sheesh.cfg](/src/source/compiler_sheesh.cfg) | Properties | 13 | 0 | 1 | 14 |
| [src/source/setup.py](/src/source/setup.py) | Python | 2 | 0 | 0 | 2 |
| [src/source/source/LexicalAnalyzer/__init__.py](/src/source/source/LexicalAnalyzer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [src/source/source/LexicalAnalyzer/lexerpy.py](/src/source/source/LexicalAnalyzer/lexerpy.py) | Python | 120 | 18 | 21 | 159 |
| [src/source/source/LexicalAnalyzer/prepare.py](/src/source/source/LexicalAnalyzer/prepare.py) | Python | 253 | 41 | 48 | 342 |
| [src/source/source/LexicalAnalyzer/tokenclass.py](/src/source/source/LexicalAnalyzer/tokenclass.py) | Python | 156 | 10 | 24 | 190 |
| [src/source/source/Sheesh# Compiler.py](/src/source/source/Sheesh#%20Compiler.py) | Python | 290 | 32 | 79 | 401 |
| [src/source/source/SyntaxAnalyzer/__init__.py](/src/source/source/SyntaxAnalyzer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [src/source/source/SyntaxAnalyzer/fsp.py](/src/source/source/SyntaxAnalyzer/fsp.py) | Python | 296 | 0 | 33 | 329 |
| [src/source/source/SyntaxAnalyzer/grammar.py](/src/source/source/SyntaxAnalyzer/grammar.py) | Python | 355 | 44 | 55 | 454 |
| [src/source/source/SyntaxAnalyzer/parser1.py](/src/source/source/SyntaxAnalyzer/parser1.py) | Python | 50 | 1 | 10 | 61 |
| [src/source/source/SyntaxAnalyzer/parser2.py](/src/source/source/SyntaxAnalyzer/parser2.py) | Python | 2,140 | 37 | 271 | 2,448 |
| [src/source/source/SyntaxAnalyzer/parser_sheesh.py](/src/source/source/SyntaxAnalyzer/parser_sheesh.py) | Python | 1,205 | 88 | 595 | 1,888 |
| [src/source/source/SyntaxAnalyzer/random.py](/src/source/source/SyntaxAnalyzer/random.py) | Python | 50 | 0 | 1 | 51 |
| [src/source/source/SyntaxAnalyzer/syntax_analyzer.py](/src/source/source/SyntaxAnalyzer/syntax_analyzer.py) | Python | 76 | 38 | 24 | 138 |
| [src/source/source/SyntaxAnalyzer/test_grammar.py](/src/source/source/SyntaxAnalyzer/test_grammar.py) | Python | 153 | 86 | 51 | 290 |
| [src/source/source/SyntaxAnalyzer/test_parser2.py](/src/source/source/SyntaxAnalyzer/test_parser2.py) | Python | 13 | 4 | 7 | 24 |
| [src/source/source/__init__.py](/src/source/source/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [src/source/source/core/__init__.py](/src/source/source/core/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [src/source/source/core/constants.py](/src/source/source/core/constants.py) | Python | 165 | 7 | 14 | 186 |
| [src/source/source/core/error_handler.py](/src/source/source/core/error_handler.py) | Python | 374 | 11 | 35 | 420 |
| [src/source/source/helper.py](/src/source/source/helper.py) | Python | 9 | 1 | 5 | 15 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)