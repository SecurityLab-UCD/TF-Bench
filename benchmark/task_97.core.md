
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--span

# poly_type
Parametric

# signature
```haskell
span :: (a -> Bool) -> [a] -> ([a],[a])
```   

# code
```haskell
span _ xs@[]            =  (xs, xs)
span p xs@(x:xs')
         | p x          =  let (ys,zs) = span p xs' in (x:ys,zs)
         | otherwise    =  ([],xs)
```

# dependencies

