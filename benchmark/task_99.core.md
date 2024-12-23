
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--splitAt

# poly_type
Parametric

# signature
```haskell
splitAt :: Int -> [a] -> ([a],[a])
```   

# code
```haskell
splitAt n xs =  (take n xs, drop n xs)
```

# dependencies
## 0
```haskell
take :: Int -> [a] -> [a]
```
## 1
```haskell
drop :: Int -> [a] -> [a]
```
