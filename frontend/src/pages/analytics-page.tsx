import { Card } from '@/components/ui/card'

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-foreground">Analytics</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Track your performance metrics and insights.
        </p>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="border-border/50 p-6">
          <h3 className="font-bold text-foreground mb-4">Traffic Over Time</h3>
          <div className="h-48 bg-secondary/20 rounded-lg flex items-center justify-center text-muted-foreground">
            Chart placeholder
          </div>
        </Card>

        <Card className="border-border/50 p-6">
          <h3 className="font-bold text-foreground mb-4">User Distribution</h3>
          <div className="h-48 bg-secondary/20 rounded-lg flex items-center justify-center text-muted-foreground">
            Chart placeholder
          </div>
        </Card>
      </div>

      {/* Detailed Metrics */}
      <Card className="border-border/50 p-6">
        <h3 className="font-bold text-foreground mb-4">Key Metrics</h3>
        <div className="space-y-4">
          {[
            { metric: 'Page Views', value: '12,543', change: '+23%' },
            { metric: 'Bounce Rate', value: '34.2%', change: '-5%' },
            { metric: 'Avg. Session', value: '4m 23s', change: '+12%' },
          ].map((item) => (
            <div key={item.metric} className="flex items-center justify-between py-3 border-b border-border/30 last:border-0">
              <span className="text-foreground">{item.metric}</span>
              <div className="flex items-center gap-2">
                <span className="font-medium text-foreground">{item.value}</span>
                <span className="text-sm text-green-600">{item.change}</span>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
