
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--concatMap

# poly_type
Parametric

# signature
```haskell
concatMap :: (a -> [b]) -> [a] -> [b]
```   

# code
```haskell
concatMap f = foldr ((++) . f) []
```

# dependencies
## 0
```haskell
foldr :: Foldable t => (a -> b -> b) -> b -> t a -> b
```
## 1
```haskell
(++) :: [a] -> [a] -> [a]
```
## 2
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
``` 
