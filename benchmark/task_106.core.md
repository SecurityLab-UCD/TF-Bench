
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--unzip

# poly_type
Parametric

# signature
```haskell
unzip :: [(a,b)] -> ([a],[b])
```   

# code
```haskell
unzip =  foldr (\(a,b) ~(as,bs) -> (a:as,b:bs)) ([],[])
```

# dependencies
## 0
```haskell
foldr :: (a -> b -> b) -> b -> [a] -> b
```


