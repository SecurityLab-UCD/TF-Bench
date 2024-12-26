
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--(!!)

# poly_type
Parametric

# signature
```haskell
(!!) :: [a] -> Int -> a
```   

# code
```haskell
xs     !! n | n < zero =  error "negative index"
[]     !! _         =  error "too large"
(x:_)  !! zero         =  x
(_:xs) !! n         =  xs !! (n-one)
```

# dependencies
## 0
```haskell
(<) :: Ord a => a -> a -> Bool
```
## 1
```haskell
(:) :: a -> [a] -> [a]
```
## 2
```haskell
(-) :: Num a => a -> a -> a
```
## 3
```haskell
zero :: Int
```
## 4
```haskell
one :: Int
```
