
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--init

# poly_type
Parametric

# note
modified

# signature
```haskell
init :: [a] -> [a]
```   

# code
```haskell
init (x:xs)             =  x : init xs
init []                 =  error
init [x]                =  []
```

# dependencies
## 1
```haskell
(:) :: a -> [a] -> [a]
```