
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--succ-Ordering

# poly_type
Monomorphic


# signature
```haskell
f1 :: T1 -> T1
```  

# code
```haskell
f1 T2 = T3
f1 T3 = T4
f1 T4 = error "bad argument"
```

# dependencies
## 0
```haskell
data T1 = T2 | T3 | T4
```
