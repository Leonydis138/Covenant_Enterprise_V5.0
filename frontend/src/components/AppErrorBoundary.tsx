import React from 'react'

type Props = {
  children: React.ReactNode
}

type State = {
  hasError: boolean
}

export default class AppErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  componentDidCatch(error: Error) {
    console.error('Unhandled UI error:', error)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-950 text-gray-200 flex items-center justify-center p-8">
          <div className="max-w-md w-full rounded-xl border border-red-500/30 bg-red-500/10 p-6">
            <h1 className="text-lg font-semibold text-red-300 mb-2">Application Error</h1>
            <p className="text-sm text-red-100/90 mb-4">
              Something went wrong while rendering the interface.
            </p>
            <button
              type="button"
              onClick={() => window.location.reload()}
              className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white text-sm font-medium transition-colors"
            >
              Reload
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
