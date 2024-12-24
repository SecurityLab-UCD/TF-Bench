
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--atan2

# poly_type
Ad-hoc

# signature
```haskell
atan2 :: RealFloat a => a -> a -> a
```   

# code
```haskell
atan2 y x
      | x > 0            =  atan (y/x)
      | x == 0 && y > 0  =  pi/2
      | x <  0 && y > 0  =  pi + atan (y/x)
      |(x <= 0 && y < 0)            ||
       (x <  0 && isNegativeZero y) ||
       (isNegativeZero x && isNegativeZero y)
                         = -atan2 (-y) x
      | y == 0 && (x < 0 || isNegativeZero x)
                          =  pi    
      | x==0 && y==0      =  y     
      | otherwise         =  x + y
```

# dependencies
## 0
```haskell
atan :: Floating a => a -> a
```
## 1
```haskell
pi :: Floating a => a
```
## 2
```haskell
(/) :: Fractional a => a -> a -> a
```
## 3
```haskell
(+) :: Num a => a -> a -> a
```
## 4
```haskell
(-) :: Num a => a -> a -> a
```
## 5
```haskell
isNegativeZero :: RealFloat a => a -> Bool
```