
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--null

# poly_type
Parametric

# signature
```haskell
null :: [a] -> Bool
```   

# code
```haskell
null []      =  True
null (_:_)   =  False
```

# dependencies

## 0
```haskell
data Bool = False | True
```