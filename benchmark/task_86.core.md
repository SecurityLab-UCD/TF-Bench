
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--scanl1

# poly_type
Parametric

# signature
```haskell
scanl1 :: (a -> a -> a) -> [a] -> [a]
```   

# code
```haskell
scanl1 _ []             =  []
scanl1 f (x:xs)         =  scanl f x xs
```

# dependencies
## 0
```haskell
scanl :: (b -> a -> b) -> b -> [a] -> [b]
```
## 1
```haskell
(:) :: a -> [a] -> [a]
```