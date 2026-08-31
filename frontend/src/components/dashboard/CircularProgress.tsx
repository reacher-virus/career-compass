import React from 'react'

export interface CircularProgressProps {
  score: number
  size?: number
  strokeWidth?: number
  label?: string
  sublabel?: string
  isDark?: boolean
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  score,
  size = 110,
  strokeWidth = 8,
  label,
  sublabel,
  isDark = false,
}) => {
  const boundedScore = Math.max(0, Math.min(Math.round(score), 100))
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (boundedScore / 100) * circumference

  // Color mapping: Claude palette uses Coral as primary, Teal as secondary
  const getColor = (s: number) => {
    if (s >= 75) return 'stroke-[#5db872] text-[#5db872]' // Green
    if (s >= 55) return 'stroke-[#cc785c] text-[#cc785c]' // Coral
    if (s >= 40) return 'stroke-[#e8a55a] text-[#e8a55a]' // Amber
    return 'stroke-[#c64545] text-[#c64545]' // Error
  }

  return (
    <div className="flex flex-col items-center justify-center text-center font-sans select-none">
      <div
        className="relative flex items-center justify-center"
        style={{ width: size, height: size }}
      >
        <svg className="transform -rotate-90" width={size} height={size}>
          {/* Background track circle */}
          <circle
            className={isDark ? 'stroke-[#262420]' : 'stroke-[#e6dfd8]'}
            strokeWidth={strokeWidth}
            fill="transparent"
            r={radius}
            cx={size / 2}
            cy={size / 2}
          />
          {/* Progress stroke */}
          <circle
            className={`transition-all duration-700 ease-out ${getColor(boundedScore)}`}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            r={radius}
            cx={size / 2}
            cy={size / 2}
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span
            className={`font-serif text-3xl font-normal tracking-tight ${
              isDark ? 'text-[#faf9f5]' : 'text-[#141413]'
            }`}
          >
            {boundedScore}%
          </span>
        </div>
      </div>
      {label && (
        <p
          className={`mt-2.5 text-xs font-medium ${
            isDark ? 'text-[#faf9f5]' : 'text-[#141413]'
          }`}
        >
          {label}
        </p>
      )}
      {sublabel && (
        <p className="text-[11px] text-[#8e8b82] line-clamp-1 mt-0.5">
          {sublabel}
        </p>
      )}
    </div>
  )
}
