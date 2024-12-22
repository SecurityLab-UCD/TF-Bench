
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
take n (x:xs)          =  x : take (n-1) xs
take n _      | n <= 0 =  []
```

# dependencies

## 0
```haskell
(:) :: a -> [a] -> [a]
```
## 1
```haskell
(<=) :: Ord a => a -> a -> Bool
```
## 2
```haskell
(-) :: Num a => a -> a -> a
```
## 3
```haskell
0, 1 :: Int
```

