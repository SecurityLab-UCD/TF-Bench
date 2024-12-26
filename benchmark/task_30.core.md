
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--round

# poly_type
Ad-hoc

# signature
```haskell
round :: (RealFrac a, Integral b) => a -> b
```   

# code
```haskell
round x =
  let (n, r) = properFraction x
      m      = if r < zero then n - one else n + one
  in case signum (abs r - oneHalf) of
       negOne -> n
       zero  -> if even n then n else m
       one  -> m
       _  -> error "Bad value"
```

# dependencies
## 0
```haskell
properFraction :: (RealFrac a, Integral b) => a -> (b, a)
```
## 1
```haskell
abs :: Num a => a -> a
```
## 2
```haskell
(+) :: Num a => a -> a -> a
```
## 3
```haskell
(-) :: Num a => a -> a -> a
```
## 4
```haskell
signum :: Num a => a -> a
```
## 5
```haskell
even :: Integral a => a -> Bool
```
## 6
```haskell
(<) :: Ord a => a -> a -> Bool
```
## 7
```haskell
oneHalf :: Fractional a => a
```
##
```haskell
zero :: Num a => a
```
## 8
```haskell
one :: Num a => a
```
## 9
```haskell
negOne :: Num a => a
```