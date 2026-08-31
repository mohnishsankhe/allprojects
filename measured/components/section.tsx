import type { ReactNode } from 'react'

export function SectionLabel({ children }: { children: ReactNode }) {
  return <p className="label text-ink-soft">{children}</p>
}

export function Section({
  id,
  children,
  className = '',
  labelledBy,
}: {
  id: string
  children: ReactNode
  className?: string
  labelledBy?: string
}) {
  return (
    <section
      id={id}
      data-section={id}
      aria-labelledby={labelledBy}
      className={`scroll-mt-16 px-5 sm:px-8 lg:px-12 ${className}`}
    >
      <div className="mx-auto w-full max-w-6xl">{children}</div>
    </section>
  )
}
