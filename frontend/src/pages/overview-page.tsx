import { Card } from '@/components/ui/card'

export default function OverviewPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-foreground">Overview</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Welcome back! Here's your dashboard overview.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { label: 'Total Users', value: '1,234', trend: '+12%' },
          { label: 'Revenue', value: '$45,231', trend: '+8%' },
          { label: 'Conversions', value: '2.4%', trend: '+4%' },
        ].map((stat) => (
          <Card key={stat.label} className="border-border/50 p-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{stat.label}</p>
              <div className="flex items-end justify-between">
                <p className="text-3xl font-bold text-foreground">
                  {stat.value}
                </p>
                <span className="text-sm text-green-600 font-medium">
                  {stat.trend}
                </span>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Content Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="border-border/50 p-6">
          <h3 className="font-bold text-foreground mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-border/30 last:border-0">
                <span className="text-sm text-foreground">Activity item {i}</span>
                <span className="text-xs text-muted-foreground">2 hours ago</span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="border-border/50 p-6">
          <h3 className="font-bold text-foreground mb-4">Quick Stats</h3>
          <div className="space-y-3">
            {['Engagement', 'Performance', 'Growth'].map((stat) => (
              <div key={stat} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-foreground">{stat}</span>
                  <span className="text-muted-foreground">75%</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full w-3/4 bg-primary rounded-full" />
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  )
}
