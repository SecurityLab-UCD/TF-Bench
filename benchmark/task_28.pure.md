
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--properFraction

# poly_type
Ad-hoc

# signature
```haskell
f1 :: (T1 a, T2 b) => a -> (b,a)
```   

# code
```haskell
f1 (x:%y) = (f2 (f3 q), r:%y)
                          where (q,r) = f4 x y
```

# dependencies
## 0
```haskell
f4 :: T2 a => a -> a -> (a,a)
```
## 1
```haskell
f3 :: T2 :: a -> T3
```
## 2
```haskell
f2 :: T2 :: T3 -> a
```
## 2
```haskell
(:%) :: T1 a => T3 -> T3 -> a
```

