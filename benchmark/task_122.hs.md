
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--readFile

# poly_type
Monomorphic

# signature
```haskell
readFile :: FilePath -> IO String
```   

# code
```haskell
readFile name   =  openFile name ReadMode >>= hGetContents
```

# dependencies
## 0
```haskell
openFile :: FilePath -> IOMode -> IO Handle
```
## 1
```haskell
(>>=) :: IO a -> (a -> IO b) -> IO b
```
## 2
```haskell
hGetContents :: Handle -> IO String
```
## 3
```haskell
data IOMode = ReadMode | WriteMode | AppendMode | ReadWriteMode
```
