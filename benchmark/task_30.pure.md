
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--round

# poly_type
Ad-hoc

# signature
```haskell
f1 :: (T1 a, T2 b) => a -> b
```   

# code
```haskell
f1 x             =  let (n,r) = f2 x
                               m     = if r < 0 then n - 1 else n + 1
                           in case f4 (f3 r - 0.5) of
                                -1 -> n
                                0  -> if f5 n then n else m
                                1  -> m
                                _  -> error "Bad value"
```

# dependencies
## 0
```haskell
f2 :: (T1 a, T2 b) => a -> (b, a)
```
## 1
```haskell
f3 :: T3 a => a -> a
```
## 2
```haskell
(+) :: T3 a => a -> a -> a
```
## 3
```haskell
(-) :: T3 a => a -> a -> a
```
## 4
```haskell
f4 :: T3 a => a -> a
```
## 5
```haskell
f5 :: T2 a => a -> Bool
```

