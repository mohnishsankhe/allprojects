'use client'

import { useEffect, useRef, useState, type ReactNode } from 'react'

/**
 * Sets `data-inview="true"` on its wrapper the first time it scrolls into
 * view, and nothing else. CSS decides what that means.
 *
 * Its children are server-rendered, so no copy or config reaches the client
 * bundle — this ships an observer, not content.
 */
export function InView({ children, threshold = 0.25 }: { children: ReactNode; threshold?: number }) {
  const ref = useRef<HTMLDivElement>(null)
  const [inView, setInView] = useState(false)

  useEffect(() => {
    const node = ref.current
    if (!node) return
    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting)) return
        setInView(true)
        observer.disconnect()
      },
      { threshold },
    )
    observer.observe(node)
    return () => observer.disconnect()
  }, [threshold])

  return (
    <div ref={ref} data-inview={inView ? 'true' : 'false'} className="mx-auto w-full max-w-6xl">
      {children}
    </div>
  )
}
