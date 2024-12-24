
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--interact

# poly_type
Monomorphic

# signature
```haskell
interact :: (String -> String) -> IO ()
```   

# code
```haskell
interact f = getContents >>= \s -> putStr (f s)
```

# dependencies
## 0
```haskell
putStr :: String -> IO ()
```
## 1
```haskell
getContents :: IO String
```
## 2
```haskell
(>>=) :: IO a -> (a -> IO b) -> IO b
```

