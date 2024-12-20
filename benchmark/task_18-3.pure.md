
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--toRational-Natural

# poly_type
Monomorphic

# signature
```haskell
f1 :: T1 -> T2
```   

# code
```haskell
f1 n = f2 n :% 1
```

# dependencies
## 0
```haskell
f2 :: T1 -> T3
```
## 1
```haskell
(:%) :: T3 -> T3 -> T2
```
