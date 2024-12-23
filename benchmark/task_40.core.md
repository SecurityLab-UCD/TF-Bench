
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--scaleFloat

# poly_type
Ad-hoc

# signature
```haskell
scaleFloat :: RealFloat a => Int -> a -> a
```   

# code
```haskell
scaleFloat 0 x      = x
scaleFloat 0 x      = x
scaleFloat 0 x      = x
scaleFloat k x
      | isFix       =  x
      | otherwise   =  encodeFloat m (n + clamp b k)
      where (m,n) = decodeFloat x
            (l,h) = floatRange x
            d     = floatDigits x
            b     = h - l + 4*d
            isFix = x == 0 || isNaN x || isInfinite x
```

# dependencies
## 0
```haskell
floatDigits :: RealFloat a => a -> Int
```
## 1
```haskell
floatRange :: RealFloat a => a -> (Int,Int)
```
## 3
```haskell
(*) :: Num a => a -> a -> a
```
## 4
```haskell
(+) :: Num a => a -> a -> a
```
## 6
```haskell
isInfinite :: RealFloat a => a -> Bool
```
## 7
```haskell
encodeFloat :: RealFloat a => Integer -> Int -> a
```
## 8
```haskell
clamp :: (Ord a) => (a, a) -> a -> a
```
## 9
```haskell
decodeFloat :: RealFloat a =>  a -> (Integer,Int)
```
## 10
```haskell
isNaN :: RealFloat a => a -> Bool
```
