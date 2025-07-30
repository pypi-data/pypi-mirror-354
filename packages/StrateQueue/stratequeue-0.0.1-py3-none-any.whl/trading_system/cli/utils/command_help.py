"""Command Help Utilities

Provides enhanced help descriptions and epilogs for individual commands
with colors, emojis, and consistent formatting.
"""

from .color_formatter import ColorFormatter

# Global formatter instance
_formatter = ColorFormatter()


def create_deploy_help() -> str:
    """Create enhanced help description for deploy command"""
    lines = []
    
    # Header
    lines.append(_formatter.title("🚀 Deploy Command") + " - " + 
                _formatter.description("Start strategies with live market data"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    
    # Description
    lines.append(_formatter.description("Launch trading strategies with real market data and optional execution."))
    lines.append(_formatter.description("Choose between paper trading (simulation), live trading (real money),"))
    lines.append(_formatter.description("or signal-only mode. Supports single strategies or multi-strategy portfolios."))
    lines.append("")
    
    return "\n".join(lines)


def create_deploy_epilog() -> str:
    """Create enhanced epilog for deploy command"""
    lines = []
    
    # Required parameters section
    lines.append(_formatter.subtitle("📋 Required:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('--strategy')}     {_formatter.description('Python strategy file (e.g., sma.py)')}")
    lines.append("")
    
    # Execution modes section
    lines.append(_formatter.subtitle("🎯 Execution Modes:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('--no-trading')}  {_formatter.description('Generate signals only (safe for testing, default)')}")
    lines.append(f"  {_formatter.highlight('--paper')}       {_formatter.description('Simulate trading with fake money')}")
    lines.append(f"  {_formatter.highlight('--live')}        {_formatter.warning('Execute real trades with real money!')}")
    lines.append("")
    
    # Common deployment patterns
    lines.append(_formatter.subtitle("💡 Common Deployments:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Test a strategy safely')}")
    lines.append(f"  {_formatter.command('stratequeue deploy --strategy sma.py --no-trading')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Paper trade with specific symbol and broker')}")
    lines.append(f"  {_formatter.command('stratequeue deploy --strategy momentum.py --symbols AAPL --broker alpaca')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Deploy multiple strategies with custom allocations')}")
    lines.append(f"  {_formatter.command('stratequeue deploy --strategy sma.py,rsi.py --allocation 0.7,0.3')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Run in background for remote management')}")
    lines.append(f"  {_formatter.command('stratequeue deploy --strategy trend.py --daemon')}")
    lines.append("")
    
    # Key configuration tips
    lines.append(_formatter.subtitle("⚙️  Configuration Tips:"))
    lines.append("")
    lines.append(f"  • {_formatter.description('Default mode: --no-trading (signals only)')}")
    lines.append(f"  • {_formatter.description('Default symbols: AAPL')}")
    lines.append(f"  • {_formatter.description('Default data source: demo (use --data-source for real data)')}")
    lines.append(f"  • {_formatter.description('Default duration: 60 minutes (use --duration to change)')}")
    lines.append(f"  • {_formatter.description('Use --daemon for background execution with remote control')}")
    lines.append("")
    
    # Footer
    lines.append(_formatter.muted("─" * 80))
    lines.append(_formatter.success("💡 Safe by default! No-trading mode ensures you test strategies first."))
    
    return "\n".join(lines)


def create_pause_help() -> str:
    """Create enhanced help description for pause command"""
    lines = []
    
    lines.append(_formatter.title("⏸️  Pause Command") + " - " + 
                _formatter.description("Pause a specific running strategy"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Stops signal generation for the specified strategy while keeping"))
    lines.append(_formatter.description("all current positions intact. Useful for temporarily halting"))
    lines.append(_formatter.description("a strategy without liquidating positions."))
    lines.append("")
    
    return "\n".join(lines)


def create_pause_epilog() -> str:
    """Create enhanced epilog for pause command"""
    lines = []
    
    lines.append(_formatter.subtitle("📋 Required:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('strategy_id')}    {_formatter.description('Strategy identifier to pause')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("💡 Usage Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Pause a strategy by ID')}")
    lines.append(f"  {_formatter.command('stratequeue pause sma_strategy')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Check what would be paused (safe preview)')}")
    lines.append(f"  {_formatter.command('stratequeue pause momentum_bot --dry-run')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🎯 What Happens:"))
    lines.append("")
    lines.append(f"  ✅ {_formatter.description('Strategy stops generating new buy/sell signals')}")
    lines.append(f"  ✅ {_formatter.description('Current positions remain exactly as they are')}")
    lines.append(f"  ✅ {_formatter.description('Market data continues to be received')}")
    lines.append(f"  ✅ {_formatter.description('Strategy can be resumed at any time')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🔄 Next Steps:"))
    lines.append("")
    lines.append(f"  {_formatter.description('Resume trading:')} {_formatter.command('stratequeue resume <strategy_id>')}")
    lines.append(f"  {_formatter.description('Check status:')} {_formatter.command('stratequeue status')}")
    lines.append("")
    
    return "\n".join(lines)


def create_remove_help() -> str:
    """Create enhanced help description for remove command"""
    lines = []
    
    lines.append(_formatter.title("🗑️  Remove Command") + " - " + 
                _formatter.description("Remove a strategy from multi-strategy system"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Permanently removes a specific strategy from a running multi-strategy"))
    lines.append(_formatter.description("system. Handles position liquidation or redistribution to remaining"))
    lines.append(_formatter.description("strategies. Cannot remove the last strategy (use stop instead)."))
    lines.append("")
    
    return "\n".join(lines)


def create_remove_epilog() -> str:
    """Create enhanced epilog for remove command"""
    lines = []
    
    lines.append(_formatter.subtitle("💡 Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Remove strategy and liquidate positions')}")
    lines.append(f"  {_formatter.command('stratequeue remove momentum --liquidate')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Remove and rebalance remaining strategies')}")
    lines.append(f"  {_formatter.command('stratequeue remove sma --rebalance')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Preview removal (dry-run)')}")
    lines.append(f"  {_formatter.command('stratequeue remove strategy_name --dry-run')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("⚖️  Position Handling:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('--liquidate')}   {_formatter.description('Sell all positions (convert to cash)')}")
    lines.append(f"  {_formatter.highlight('Default')}       {_formatter.description('Transfer positions to remaining strategies')}")
    lines.append("")
    
    return "\n".join(lines)


def create_rebalance_help() -> str:
    """Create enhanced help description for rebalance command"""
    lines = []
    
    lines.append(_formatter.title("⚖️  Rebalance Command") + " - " + 
                _formatter.description("Rebalance portfolio allocations"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Adjust portfolio allocations between strategies in real-time."))
    lines.append(_formatter.description("Supports equal-weight or custom allocation rebalancing."))
    lines.append("")
    
    return "\n".join(lines)


def create_rebalance_epilog() -> str:
    """Create enhanced epilog for rebalance command"""
    lines = []
    
    lines.append(_formatter.subtitle("💡 Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Equal weight rebalancing')}")
    lines.append(f"  {_formatter.command('stratequeue rebalance --allocations=equal')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Custom allocations')}")
    lines.append(f"  {_formatter.command('stratequeue rebalance --allocations=0.5,0.3,0.2')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Specify strategy order')}")
    lines.append(f"  {_formatter.command('stratequeue rebalance --allocations=0.6,0.4 --strategy-ids=sma,momentum')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🎯 Rebalance Targets:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('--target=portfolio')}  {_formatter.description('Update allocation percentages only')}")
    lines.append(f"  {_formatter.highlight('--target=positions')}  {_formatter.description('Rebalance actual positions')}")
    lines.append(f"  {_formatter.highlight('--target=both')}       {_formatter.description('Update both (default)')}")
    lines.append("")
    
    return "\n".join(lines)


def create_resume_help() -> str:
    """Create enhanced help description for resume command"""
    lines = []
    
    lines.append(_formatter.title("▶️  Resume Command") + " - " + 
                _formatter.description("Resume a paused strategy"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Reactivates signal generation for a previously paused strategy."))
    lines.append(_formatter.description("Strategy resumes exactly where it left off with all positions intact."))
    lines.append(_formatter.description("Counterpart to the pause command."))
    lines.append("")
    
    return "\n".join(lines)


def create_resume_epilog() -> str:
    """Create enhanced epilog for resume command"""
    lines = []
    
    lines.append(_formatter.subtitle("📋 Required:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('strategy_id')}    {_formatter.description('Strategy identifier to resume')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("💡 Usage Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Resume a paused strategy')}")
    lines.append(f"  {_formatter.command('stratequeue resume sma_strategy')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Preview resume action')}")
    lines.append(f"  {_formatter.command('stratequeue resume momentum_bot --dry-run')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🎯 What Happens:"))
    lines.append("")
    lines.append(f"  ✅ {_formatter.description('Strategy starts generating buy/sell signals again')}")
    lines.append(f"  ✅ {_formatter.description('Picks up with current market conditions')}")
    lines.append(f"  ✅ {_formatter.description('All existing positions remain intact')}")
    lines.append(f"  ✅ {_formatter.description('Trading resumes with full functionality')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("📝 Prerequisites:"))
    lines.append("")
    lines.append(f"  • {_formatter.description('Strategy must be currently paused')}")
    lines.append(f"  • {_formatter.description('Trading system must be running')}")
    lines.append("")
    
    return "\n".join(lines)


def create_stop_help() -> str:
    """Create enhanced help description for stop command"""
    lines = []
    
    lines.append(_formatter.title("🛑 Stop Command") + " - " + 
                _formatter.description("Shutdown the entire trading system"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Terminates all running strategies and shuts down the trading system."))
    lines.append(_formatter.description("Choose between graceful shutdown (keeps positions) or full liquidation."))
    lines.append(_formatter.description("This stops the entire system, not just individual strategies."))
    lines.append("")
    
    return "\n".join(lines)


def create_stop_epilog() -> str:
    """Create enhanced epilog for stop command"""
    lines = []
    
    lines.append(_formatter.subtitle("🛑 Shutdown Options:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('Default')}       {_formatter.description('Graceful shutdown, preserve all positions')}")
    lines.append(f"  {_formatter.highlight('--force')}       {_formatter.description('Immediate shutdown, bypass safety checks')}")
    lines.append(f"  {_formatter.highlight('--liquidate')}   {_formatter.description('Sell all positions before shutdown')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("💡 Common Usage:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Normal shutdown (recommended)')}")
    lines.append(f"  {_formatter.command('stratequeue stop')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Emergency shutdown')}")
    lines.append(f"  {_formatter.command('stratequeue stop --force')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Liquidate everything and stop')}")
    lines.append(f"  {_formatter.command('stratequeue stop --liquidate')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Preview shutdown actions')}")
    lines.append(f"  {_formatter.command('stratequeue stop --dry-run')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("⚠️  Important:"))
    lines.append("")
    lines.append(f"  • {_formatter.warning('This stops ALL running strategies')}")
    lines.append(f"  • {_formatter.description('Use')} {_formatter.command('pause')} {_formatter.description('to temporarily halt individual strategies')}")
    lines.append(f"  • {_formatter.description('System must be redeployed after stopping')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🔄 Aliases:"))
    lines.append(f"  {_formatter.command('shutdown')}, {_formatter.command('kill')}")
    lines.append("")
    
    return "\n".join(lines)


def create_list_help() -> str:
    """Create enhanced help description for list command"""
    lines = []
    
    lines.append(_formatter.title("📋 List Command") + " - " + 
                _formatter.description("Discover available system components"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Shows all supported brokers, data sources, and time granularities"))
    lines.append(_formatter.description("available for use in strategy deployment. Essential for discovering"))
    lines.append(_formatter.description("what options are supported before configuring your strategies."))
    lines.append("")
    
    return "\n".join(lines)


def create_list_epilog() -> str:
    """Create enhanced epilog for list command"""
    lines = []
    
    lines.append(_formatter.subtitle("📋 Available Categories:"))
    lines.append("")
    lines.append(f"  {_formatter.highlight('brokers')}        {_formatter.description('Trading brokers (alpaca, kraken, etc.)')}")
    lines.append(f"  {_formatter.highlight('granularities')}  {_formatter.description('Time intervals (1m, 5m, 1h, etc.)')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("💡 Discovery Commands:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# See all supported brokers')}")
    lines.append(f"  {_formatter.command('stratequeue list brokers')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# See available time granularities')}")
    lines.append(f"  {_formatter.command('stratequeue list granularities')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🔄 Workflow:"))
    lines.append("")
    lines.append(f"  1. {_formatter.description('Use list to discover options')}")
    lines.append(f"  2. {_formatter.description('Use')} {_formatter.command('setup')} {_formatter.description('to configure brokers')}")
    lines.append(f"  3. {_formatter.description('Use')} {_formatter.command('deploy')} {_formatter.description('with discovered options')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🔄 Aliases:"))
    lines.append(f"  {_formatter.command('ls')}, {_formatter.command('show')}")
    lines.append("")
    
    return "\n".join(lines)


def create_status_help() -> str:
    """Create enhanced help description for status command"""
    lines = []
    
    lines.append(_formatter.title("🔍 Status Command") + " - " + 
                _formatter.description("Check system and broker status"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Check the health of your trading system, brokers, and connections."))
    lines.append(_formatter.description("Verify broker credentials and system readiness before trading."))
    lines.append("")
    
    return "\n".join(lines)


def create_status_epilog() -> str:
    """Create enhanced epilog for status command"""
    lines = []
    
    lines.append(_formatter.subtitle("💡 Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Check overall system status')}")
    lines.append(f"  {_formatter.command('stratequeue status')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Check specific broker')}")
    lines.append(f"  {_formatter.command('stratequeue status --broker alpaca')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🎯 Aliases:"))
    lines.append("")
    lines.append(f"  {_formatter.command('stratequeue check')}")
    lines.append(f"  {_formatter.command('stratequeue health')}")
    lines.append("")
    
    return "\n".join(lines)


def create_setup_help() -> str:
    """Create enhanced help description for setup command"""
    lines = []
    
    lines.append(_formatter.title("⚙️  Setup Command") + " - " + 
                _formatter.description("Configure brokers and system settings"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Configure broker credentials and system settings for trading."))
    lines.append(_formatter.description("Interactive setup guide for first-time users and credential updates."))
    lines.append("")
    
    return "\n".join(lines)


def create_setup_epilog() -> str:
    """Create enhanced epilog for setup command"""
    lines = []
    
    lines.append(_formatter.subtitle("💡 Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Interactive setup wizard')}")
    lines.append(f"  {_formatter.command('stratequeue setup')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Setup specific broker')}")
    lines.append(f"  {_formatter.command('stratequeue setup broker alpaca')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🎯 Aliases:"))
    lines.append("")
    lines.append(f"  {_formatter.command('stratequeue config')}")
    lines.append(f"  {_formatter.command('stratequeue configure')}")
    lines.append("")
    
    return "\n".join(lines)


def create_webui_help() -> str:
    """Create enhanced help description for webui command"""
    lines = []
    
    lines.append(_formatter.title("🌐 WebUI Command") + " - " + 
                _formatter.description("Start the web interface"))
    lines.append("")
    lines.append(_formatter.muted("─" * 80))
    lines.append("")
    lines.append(_formatter.description("Launch the browser-based dashboard for visual trading management."))
    lines.append(_formatter.description("Monitor strategies, positions, and performance in real-time."))
    lines.append("")
    
    return "\n".join(lines)


def create_webui_epilog() -> str:
    """Create enhanced epilog for webui command"""
    lines = []
    
    lines.append(_formatter.subtitle("💡 Examples:"))
    lines.append("")
    lines.append(f"  {_formatter.muted('# Start web interface (default port 8000)')}")
    lines.append(f"  {_formatter.command('stratequeue webui')}")
    lines.append("")
    lines.append(f"  {_formatter.muted('# Custom port')}")
    lines.append(f"  {_formatter.command('stratequeue webui --port 9000')}")
    lines.append("")
    
    lines.append(_formatter.subtitle("🎯 Aliases:"))
    lines.append("")
    lines.append(f"  {_formatter.command('stratequeue web')}")
    lines.append(f"  {_formatter.command('stratequeue ui')}")
    lines.append("")
    
    return "\n".join(lines)


# Mapping of command names to help functions
COMMAND_HELP_MAP = {
    'deploy': {
        'description': create_deploy_help,
        'epilog': create_deploy_epilog
    },
    'pause': {
        'description': create_pause_help,
        'epilog': create_pause_epilog
    },
    'resume': {
        'description': create_resume_help,
        'epilog': create_resume_epilog
    },
    'stop': {
        'description': create_stop_help,
        'epilog': create_stop_epilog
    },
    'remove': {
        'description': create_remove_help,
        'epilog': create_remove_epilog
    },
    'rebalance': {
        'description': create_rebalance_help,
        'epilog': create_rebalance_epilog
    },
    'list': {
        'description': create_list_help,
        'epilog': create_list_epilog
    },
    'status': {
        'description': create_status_help,
        'epilog': create_status_epilog
    },
    'setup': {
        'description': create_setup_help,
        'epilog': create_setup_epilog
    },
    'webui': {
        'description': create_webui_help,
        'epilog': create_webui_epilog
    }
}


def get_command_help(command_name: str) -> dict:
    """
    Get enhanced help content for a command
    
    Args:
        command_name: Name of the command
        
    Returns:
        Dictionary with 'description' and 'epilog' keys
    """
    if command_name in COMMAND_HELP_MAP:
        help_funcs = COMMAND_HELP_MAP[command_name]
        return {
            'description': help_funcs['description'](),
            'epilog': help_funcs['epilog']()
        }
    
    # Default help for commands without custom help
    return {
        'description': f"📋 {command_name.title()} Command",
        'epilog': f"Use {_formatter.command(f'stratequeue {command_name} --help')} for more information."
    } 