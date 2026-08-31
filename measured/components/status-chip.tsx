import Link from 'next/link'
import { claim, resolveTarget, type ClaimId, type ClaimStatus } from '@/content/manifest'

const STATUS_STYLE: Record<ClaimStatus, string> = {
  MEASURED: 'text-status-measured border-status-measured/35 bg-status-measured/[0.06]',
  PLANNED: 'text-status-planned border-status-planned/35 bg-status-planned/[0.07]',
  PROVISIONAL: 'text-status-provisional border-ink-line bg-ink-wash',
}

/**
 * Every checkable statement on the site wears one of these, and every chip is
 * a link into the manifest row it comes from. If a line has no chip, it is not
 * making a claim.
 */
export function StatusChip({
  claimId,
  note,
  className = '',
}: {
  claimId: ClaimId
  note?: string | null
  className?: string
}) {
  const entry = claim(claimId)
  const target = resolveTarget(entry)
  const suffix = note ?? (entry.status === 'PLANNED' && target ? target : null)

  return (
    <Link
      href={`/receipts#${entry.id}`}
      className={`label inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 transition-opacity hover:opacity-70 ${STATUS_STYLE[entry.status]} ${className}`}
    >
      <span>{entry.status}</span>
      {suffix ? <span className="font-normal normal-case tracking-normal">— {suffix}</span> : null}
    </Link>
  )
}
