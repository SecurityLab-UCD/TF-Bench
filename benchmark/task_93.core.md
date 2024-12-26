
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--take

# poly_type
Parametric

# signature
```haskell
take :: Int -> [a] -> [a]
```   

# code
```haskell
take _ []              =  []
take n (x:xs)          =  x : take (n-one) xs
take n _      | n <= zero =  []
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
one :: Int
```


