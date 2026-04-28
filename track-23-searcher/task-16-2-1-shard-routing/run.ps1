$ErrorActionPreference = 'Stop'
$TaskDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $TaskDir '..\..')
$Module = 'track-23-searcher/task-16-2-1-shard-routing'
Set-Location $RepoRoot
mvn -q -pl $Module dependency:copy-dependencies package
$InputFile = Join-Path $TaskDir 'samples\input.jsonl'
if (!(Test-Path $InputFile)) {
    $InputFile = Join-Path $TaskDir 'samples\input-1.jsonl'
}
if (Test-Path $InputFile) {
    Get-Content $InputFile | java -cp "$TaskDir\target\classes;$TaskDir\target\dependency\*" Main
} else {
    java -cp "$TaskDir\target\classes;$TaskDir\target\dependency\*" Main
}
