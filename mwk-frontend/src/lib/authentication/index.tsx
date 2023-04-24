/**
 * Switch to the next input on user press 'Enter'
 * @param {Promise<(import('react').SyntheticEvent} event
 */
export function handleEnter(event: React.KeyboardEvent<HTMLInputElement>) {
  if (event.key === 'Enter' || event.key === 'Space') {
    const form = event.currentTarget.form as HTMLFormElement
    const index = Array.from(form.elements).indexOf(event.currentTarget)
    if (index >= 0) {
      const nextElement = form.elements[index + 2] as HTMLInputElement
      if (nextElement) {
        nextElement.focus()
        event.preventDefault()
      }
    }
  }
}
