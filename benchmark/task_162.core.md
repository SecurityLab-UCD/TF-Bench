
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--reverse

# poly_type
Parametric

# signature
```haskell
reverse :: [a] -> [a]
```   

# code
```haskell
reverse = foldl (flip (:)) []
```

# dependencies
## 0
```haskell
foldl :: (b -> a -> b) -> b -> [a] -> b
```
## 1
```haskell
flip :: (a -> b -> c) -> b -> a -> c
```
## 2
```haskell
(:) :: a -> [a] -> [a]
```
