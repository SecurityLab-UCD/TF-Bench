
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--atan2

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => a -> a -> a
```   

# code
```haskell
f1 y x
      | x > 0            =  f2 (y/x)
      | x == 0 && y > 0  =  c1/2
      | x <  0 && y > 0  =  c1 + f2 (y/x)
      |(x <= 0 && y < 0)            ||
       (x <  0 && f3 y) ||
       (f3 x && f3 y)
                         = -f1 (-y) x
      | y == 0 && (x < 0 || f3 x)
                          =  c1    
      | x==0 && y==0      =  y     
      | otherwise         =  x + y
```

# dependencies
## 0
```haskell
f2 :: T2 a => a -> a
```
## 1
```haskell
c1 :: T2 a => a
```
## 2
```haskell
(/) :: T3 a => a -> a -> a
```
## 3
```haskell
(+) :: T4 a => a -> a -> a
```
## 4
```haskell
(-) :: T4 a => a -> a -> a
```
## 5
```haskell
f3 :: T1 a => a -> Bool
```