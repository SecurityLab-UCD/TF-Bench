
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--scanr1

# poly_type
Parametric

# signature
```haskell
scanr1 :: (a -> a -> a) -> [a] -> [a]
```   

# code
```haskell
scanr1 _ []             =  []
scanr1 _ [x]            =  [x]
scanr1 f (x:xs)         =  f x q : qs
                           where qs@(q:_) = scanr1 f xs
```

# dependencies
