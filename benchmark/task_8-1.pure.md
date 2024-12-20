
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--toEnum-Bool

# poly_type
Monomorphic

# signature
```haskell
f1 :: T2 -> T1
```   

# code
```haskell
f1 n | n == 0    = T3
     | n == 1    = T4
     | otherwise = error "bad argument"
```

# dependencies
## 0
```haskell
data T1 = T3 | T4
```
