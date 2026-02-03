import * as React from 'react';

interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
}

const Switch = React.forwardRef<HTMLInputElement, SwitchProps>(
  ({ checked, onCheckedChange, className, ...props }, ref) => {
    const [isChecked, setIsChecked] = React.useState(!!checked);

    React.useEffect(() => {
      if (checked !== undefined) {
        setIsChecked(checked);
      }
    }, [checked]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const newChecked = e.target.checked;
      setIsChecked(newChecked);
      if (onCheckedChange) {
        onCheckedChange(newChecked);
      }
    };

    return (
      <div className="relative inline-block w-12 h-7 align-middle select-none">
        <input
          ref={ref}
          type="checkbox"
          checked={isChecked}
          onChange={handleChange}
          className={`sr-only ${className}`}
          {...props}
        />
        <div
          onClick={() => {
            const newChecked = !isChecked;
            setIsChecked(newChecked);
            if (onCheckedChange) {
              onCheckedChange(newChecked);
            }
          }}
          className={`block w-12 h-7 rounded-full cursor-pointer transition-colors ${
            isChecked 
              ? 'bg-primary-500 dark:bg-primary-600' 
              : 'bg-slate-300 dark:bg-slate-600'
          }`}
        >
          <div
            className={`absolute left-0.5 top-0.5 bg-white dark:bg-slate-200 w-6 h-6 rounded-full transition-transform ${
              isChecked ? 'transform translate-x-5' : ''
            }`}
          />
        </div>
      </div>
    );
  }
);
Switch.displayName = 'Switch';

export { Switch };