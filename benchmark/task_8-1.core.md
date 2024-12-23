
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--toEnum-Bool

# poly_type
Monomorphic

# signature
```haskell
toEnum :: Int -> Bool
```   

# code
```haskell
toEnum n | n == 0    = False
         | n == 1    = True
         | otherwise = error "bad argument"
```

# dependencies
## 0
```haskell
data Bool = False | True
```
