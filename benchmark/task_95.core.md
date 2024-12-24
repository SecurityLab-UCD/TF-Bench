
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--takeWhile

# poly_type
Parametric

# signature
```haskell
takeWhile :: (a -> Bool) -> [a] -> [a]
```   

# code
```haskell
takeWhile _ []          =  []
takeWhile p (x:xs)
            | p x       =  x : takeWhile p xs
            | otherwise =  []
```

# dependencies
## 0
```haskell
(:) :: a -> [a] -> [a]
```
