
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--signum-Int

# poly_type
Monomorphic

# signature
```haskell
f1 :: T1 -> T1
```   

# code
```haskell
f1 n | f2 n 0 = f4 1
     | f3 n 0 = 0
     | otherwise   = 1
```

# dependencies
## 0
```haskell
f4 :: T1 -> T1
```
## 1
```haskell
f2 :: T1 -> T1 -> Bool
```
## 2
```haskell
f3 :: T1 -> T1 -> Bool
```
## 3
```haskell
type T1 = Int
```