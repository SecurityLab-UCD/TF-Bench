
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--abs-Int

# poly_type
Monomorphic

# signature
```haskell
f1 :: T1 -> T1
```   

# code
```haskell
f1 n  = if n > 0 then n else f2 n
```

# dependencies
## 0
```haskell
(>) :: T1 -> T1 -> Bool
```
## 1
```haskell
f2 :: T1 -> T1
```
