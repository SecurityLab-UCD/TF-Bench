
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--tail

# poly_type
Parametric

# note
modified

# signature
```haskell
tail :: [a] -> [a]
```   

# code
```haskell
tail (_:xs)             =  xs
tail []                 =  error
```

# dependencies
