
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--iterate

# poly_type
Parametric

# signature
```haskell
iterate :: (a -> a) -> a -> [a]
```   

# code
```haskell
iterate f x =  x : iterate f (f x)
```

# dependencies
```haskell
(:) :: a -> [a] -> [a]
```