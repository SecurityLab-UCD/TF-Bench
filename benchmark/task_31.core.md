
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--ceiling

# poly_type
Ad-hoc

# signature
```haskell
ceiling :: (RealFrac a, Integral b) => a -> b
```   

# code
```haskell
ceiling x           =  if r > 0 then n + 1 else n
                           where (n,r) = properFraction x
```

# dependencies
## 0
```haskell
properFraction :: (RealFrac a, Integral b) => a -> (b, a)
```
## 1
```haskell
(+) :: Num a => a -> a -> a
```
## 2
```haskell
(>) :: Ord a => a -> a -> Bool
```
