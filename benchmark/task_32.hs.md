
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--floor

# poly_type
Ad-hoc

# signature
```haskell
floor :: (RealFrac a, Integral b) => a -> b
```   

# code
```haskell
floor x             =  if r < zero then n - one else n
                           where (n,r) = properFraction x
```

# dependencies
## 0
```haskell
properFraction :: (RealFrac a, Integral b) => a -> (b, a)
```
## 1
```haskell
(-) :: Num a => a -> a -> a
```
## 2
```haskell
(<) :: Ord a => a -> a -> Bool
```
## 3
```haskell
zero :: Num a => a
```
## 4
```haskell
one :: Num a => a
```
