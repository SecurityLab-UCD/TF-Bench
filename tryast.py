from tfbench.hs_parser import AST

code = "f :: Ord a => [a] -> Int"
ast = AST(code)

print(ast.root)
