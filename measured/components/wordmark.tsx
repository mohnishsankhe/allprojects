import { BRAND } from '@/brand.config'

/**
 * The logo is the wordmark plus one filled dot. The dot is the only mark the
 * brand has, so it is drawn, never imaged, and it is the one place the accent
 * appears outside a measured number or a status chip.
 */
export function Wordmark({ className = '', dotClassName = '' }: { className?: string; dotClassName?: string }) {
  return (
    <span className={`inline-flex items-baseline font-medium tracking-tight ${className}`}>
      {BRAND.name}
      <span
        aria-hidden="true"
        className={`ml-[0.14em] inline-block size-[0.3em] shrink-0 translate-y-[-0.04em] rounded-full bg-accent ${dotClassName}`}
      />
    </span>
  )
}
