def linePlot(fig, cursor, args):
    ax = fig.add_subplot(111)
    for doc in cursor:
      ax.plot(doc[args.x_col], doc[args.y_col])
    ax.grid()
    ax.set_title(args.title)
    ax.set_xlabel(args.x_col)
    ax.set_ylabel(args.y_col)


def scatterPlot(fig, cursor, args):
    ax = fig.add_subplot(111)
    for doc in cursor:
      ax.scatter(doc[args.x_col], doc[args.y_col])
    ax.grid()
    ax.set_title(args.title)
    ax.set_xlabel(args.x_col)
    ax.set_ylabel(args.y_col)


def histPlot(fig, cursor, args):
    ax = fig.add_subplot(111)
    for doc in cursor:
      ax.hist(doc[args.x_col],50, normed=1)
    ax.set_title(args.title)
    ax.set_xlabel(args.x_col)


def customPlot(fig, cursor, args):
    ax = fig.add_subplot(111)
    print args.custom_plot_code
    for doc in cursor:
      exec args.custom_plot_code_doc
    exec args.custom_plot_code
