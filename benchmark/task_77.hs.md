
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--last

# poly_type
Parametric

# note
modified

# signature
```haskell
last ::  [a] -> a
```   

# code
```haskell
last (_:xs)             =  last xs
last []                 =  error
last [x]                =  x
```

# dependencies
