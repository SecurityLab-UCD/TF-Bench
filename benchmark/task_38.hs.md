
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--exponent

# poly_type
Ad-hoc

# signature
```haskell
exponent :: RealFloat a => a -> Int
```   

# code
```haskell
exponent x = if m == zero then zero else n + floatDigit       
    where (m,n) = decodeFloat x
```

# dependencies
## 0
```haskell
decodeFloat :: RealFloat a => a -> (Integer, Int)
```
## 1
```haskell
floatDigits :: RealFloat a => a -> Int
```
## 2
```haskell
(+) :: Num a => a -> a -> a
```
## 3
```haskell
(==) :: Eq a => a -> a -> Bool
```
## 4
```haskell
zero :: Num a => a
```