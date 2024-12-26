
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--drop

# poly_type
Parametric

# signature
```haskell
drop :: Int -> [a] -> [a]
```   

# code
```haskell
drop _ []              =  []
drop n (_:xs)          =  drop (n-one) xs
drop n xs     | n <= zero =  xs
```

# dependencies
## 0
```haskell
(<=) :: Ord a => a -> a -> Bool
```
## 1
```haskell
(-) :: Num a => a -> a -> a
```
## 2
```haskell
zero :: Int
```
## 3
```haskell
(:) :: a -> [a] -> [a]
```
## 4
```haskell
one :: Int
```


