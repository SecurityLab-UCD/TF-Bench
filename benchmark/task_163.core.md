
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
xs     !! n | n < 0 =  error "negative index"
[]     !! _         =  error "too large"
(x:_)  !! 0         =  x
(_:xs) !! n         =  xs !! (n-1)
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
