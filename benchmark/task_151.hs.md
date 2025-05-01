
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--(^)

# poly_type
Ad-hoc

# signature
```haskell
(^) :: (Num a, Integral b) => a -> b -> a
```   

# code
```haskell
x ^ y | y < zero = error "negative"
      | y == zero = one
      | otherwise = powImpl x y
```

# dependencies
## 0
```haskell
(<) :: Ord a => a -> a -> Bool
```
## 1
```haskell
(==) :: Eq a => a -> a -> Bool
```
## 2
```haskell
powImpl :: (Num a, Integral b) => a -> b -> a
```
## 3
```haskell
zero :: Num a => a
```
## 4
```haskell
one :: Num a => a
```