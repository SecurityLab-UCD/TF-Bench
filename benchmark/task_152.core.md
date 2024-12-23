
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--(^^)

# poly_type
Ad-hoc

# signature
```haskell
(^^) :: (Fractional a, Integral b) => a -> b -> a
```   

# code
```haskell
x ^^ n =  if n >= 0 then x^n else recip (x^(negate n))
```

# dependencies
## 0
```haskell
(>=) :: Ord a => a -> a -> Bool
```
## 1
```haskell
(^) :: (Num a, Integral b) => a -> b -> a
```
## 2
```haskell
recip :: Fractional a => a -> a
```
## 3
```haskell
negate :: Num a => a -> a
```