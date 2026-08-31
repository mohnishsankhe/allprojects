import type { ClaimStatus } from '@/content/manifest'

const STYLE: Record<ClaimStatus, string> = {
  MEASURED: 'text-status-measured border-status-measured/35 bg-status-measured/[0.06]',
  PLANNED: 'text-status-planned border-status-planned/35 bg-status-planned/[0.07]',
  PROVISIONAL: 'text-status-provisional border-ink-line bg-ink-wash',
}

/** The chip without the link, for use inside something already clickable. */
export function ClaimStatusBadge({ status, className = '' }: { status: ClaimStatus; className?: string }) {
  return (
    <span className={`label inline-flex items-center rounded-full border px-2.5 py-1 ${STYLE[status]} ${className}`}>
      {status}
    </span>
  )
}
