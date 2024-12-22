
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--lines

# poly_type
Monomorphic

# signature
```haskell
lines :: String -> [String]
```   

# code
```haskell
lines "" =  []
lines s  =  cons (case break (== '\n') s of
       (l, s') -> (l, case s' of
                       []      -> []
                       _:s''   -> lines s''))
  where
    cons ~(h, t) =  h : t
```

# dependencies
## 0
```haskell
break :: (a -> Bool) -> [a] -> ([a],[a])
```
