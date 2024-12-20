
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--toRational-Int

# poly_type
Monomorphic

# signature
```haskell
f1 :: T1 -> T2
```   

# code
```haskell
f1 x = f2 x :% 1
```

# dependencies
## 0
```haskell
f2 :: T1 -> T2
```
## 1
```haskell
(:%) :: T2 -> T2 -> T3
```
## 2
```haskell
type T2 = Integer
```

