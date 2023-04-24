export const debounce = (f: any, ms: number) => {
  let isCooldown = false

  return function debounceFunction(this: any, ...args: any[]) {
    if (isCooldown) return

    f.apply(this, args)

    isCooldown = true

    setTimeout(() => (isCooldown = false), ms)
  }
}
